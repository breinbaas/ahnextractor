"""
Copyright (c) 2022 VIKTOR B.V. / Breinbaas
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. / Breinbaas PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pydantic import BaseModel
from enum import IntEnum
from typing import List, Tuple, Dict, Union, Any
import aiohttp
import numpy as np
import numpy.typing as npt
import asyncio
import warnings
from rdp import rdp

from .polyline import Polyline

class AhnVersion(IntEnum):
    AHN2 = 2
    AHN3 = 3
    # AHN4 = 4

class AhnSource(IntEnum):
    DTM = 0
    DSM = 1

AhnUrls = {
    AhnVersion.AHN2:"https://geodata.nationaalgeoregister.nl/ahn2/wms",
    AhnVersion.AHN3:"https://geodata.nationaalgeoregister.nl/ahn3/wms",    
}

AhnDTMBladIndex = {
    AhnVersion.AHN2:"ahn2_05m_int",
    AhnVersion.AHN3:"ahn3_05m_dtm"
}

AhnDSMBladIndex = {
    AhnVersion.AHN2:"ahn2_05m_ruw",
    AhnVersion.AHN3:"ahn3_05m_dsm"
}

GRIDSIZE_AHN = 0.5

class AhnExtractor(BaseModel):
    version: AhnVersion = AhnVersion.AHN3
    source: AhnSource = AhnSource.DTM
        
    def get(self, polyline: Polyline, interval: float = 5., rdp_epsilon=0.0) -> List[Dict[str, Union[float, Any]]]:
        """
        Splits the defined Polyline into sections with a length of +interval+
        :param polyline: Provide the line along which the AHN should be obtained
        :param interval: Interval after which distance in metres a new value of the AHN should be obtained
        :param rdp_epsilon: Epsilon for RDP algorithm, defaults to 0.0 (no RDP)
        :return: A list of all the AHN values in the same direction as the Polyline
        """
        line_section_lengths = self._get_geo_polyline_section_length(polyline)
        points = polyline.points  # Gets the RD coordinates for each point defined in the Polyline
        lines_ahn_data_list = []  # Set up a list such that the values along each line can be saved

        
        # For each line, get the start point, end point and the length        
        llprev = 0         
        for point_start, point_end, section_length in zip(points[:-1], points[1:], line_section_lengths):
            dx = point_end[0] - point_start[0]
            dy = point_end[1] - point_start[1]
            nls = np.arange(0, section_length, interval)
            xs = [round(point_start[0] + l / section_length * dx, 2) for l in nls]
            ys = [round(point_start[1] + l / section_length * dy, 2) for l in nls]
            ls = [round(l + llprev,2) for l in nls]
            z_ahn = [round(z, 3) for z in asyncio.run(self._async_get_ahn_of_rd_points([point_start, point_end], interval))]
            ahn_data = list(zip(ls, xs,ys,z_ahn))
            lines_ahn_data_list += ahn_data  # Save the values to the list
            llprev += section_length

        if rdp_epsilon > 0:
            final_points = [p[0] for p in rdp([(p[0], p[-1]) for p in lines_ahn_data_list], epsilon=rdp_epsilon)]
            lines_ahn_data_list = [p for p in lines_ahn_data_list if p[0] in final_points]
        
        return lines_ahn_data_list  # Return the data list

    def _get_geo_polyline_section_length(self, geo_polyline: Polyline) -> npt.NDArray[float]:
        """
        Get the length of the polyline
        """
        # Get the RD coordinates for each point defined in the Polyline
        points = np.array(geo_polyline.points)
        points_diff = np.diff(points, axis=0)  # Get the distance in x and y from point to point
        points_diff_squared = points_diff ** 2  # Square the distances
        points_squared = points_diff_squared.sum(axis=1)  # Sum the x and y distances (a**2 + b**2 = c**2)
        return np.sqrt(points_squared)  # Return the total length of the polyline according to the Pythagorean theorem


    def _get_map_payload(self, points: List[Tuple[float, float]], interval: float = 5.) -> Dict[str, str]:
        """
        Makes a dictionary to define the map parameters used by the AHN WMS service.
        Defines the bbox as a box around the line that should be drawn, with half a pixel margin.
        Defines the width and height as the amount of pixels needed to make the desired line either a diagonal of the
        resulting square, or a vertical/horizontal line
        """
        bbox = self._get_bounding_box_of_rd_points(points)
        x_min, y_min, x_max, y_max = bbox
        width, height = self._get_width_and_height_of_rd_points(points, interval, bbox)
        # The bbox is currently the outermost edges of the map. However, since the map will be filled with pixels, the
        # centre of the pixel in the top left corner will be slightly to the right and below of the bbox top left corner.
        # Let's compensate for that by adding half a pixel to the left, right, top and bottom
        if (x_max - x_min) < GRIDSIZE_AHN:  # First check whether the line is vertical
            width = 0  # Set a zero pixel width if it is
            pixel_dx = GRIDSIZE_AHN / 200
        else:  # Otherwise check what the pixel_dx is
            pixel_dx = (x_max - x_min) / width
        if (y_max - y_min) < GRIDSIZE_AHN:  # Do the same for y
            height = 0
            pixel_dy = GRIDSIZE_AHN / 200
        else:
            pixel_dy = (y_max - y_min) / height
        x_min, x_max = x_min - pixel_dx / 2., x_max + pixel_dx / 2.  # Increase the bbox size by half the pixel width
        y_min, y_max = y_min - pixel_dy / 2., y_max + pixel_dy / 2.
        bbox_compensated = x_min, y_min, x_max, y_max
        width_compensated, height_compensated = width + 1, height + 1
        return {  # Return the compensated values
            "bbox": f"{','.join(str(b) for b in bbox_compensated)}", "width": f"{width_compensated}",
            "height": f"{height_compensated}",
        }


    def _get_bounding_box_of_rd_points(self, points: List[Tuple[float, float]]) -> Tuple[float, float, float, float]:
        """
        Get the bounding box that surrounds the Polyline in RD coordinates
        :param points: The defined line
        :return: x_min, y_min, x_max, y_max
        """
        points_arr = np.array(points)
        x_min, y_min = points_arr.min(axis=0)
        x_max, y_max = points_arr.max(axis=0)
        return x_min, y_min, x_max, y_max


    def _get_width_and_height_of_rd_points(self, points: List[Tuple[float, float]], interval: float = 5.,
                                        bbox: [None, Tuple] = None):
        """
        The actual splitting of the points is done in this function. As we have already defined the bounding box, we need
        the location of each point in the split and width and height of the requested map. This function will check how
        many sections are needed to achieve the desired interval, and then create a square box using the width and height of
        the image. The location of the line drawn onto this square map is then the diagonal, which makes iteration easy and
        straightforward
        :param points: The defined line
        :param interval: Maximum length between two neighbouring points in metres
        :param bbox: Bounding box. If not defined it will be obtained
        :return: width, height
        """
        x_min, y_min, x_max, y_max = bbox or self._get_bounding_box_of_rd_points(points)
        line_length = np.linalg.norm(np.array([x_max - x_min, y_max - y_min]))
        number_of_sections = int(line_length / interval)
        return number_of_sections, number_of_sections

    async def _async_get_ahn_of_rd_points(self, points: List[Tuple[float, float]], interval: float) -> List[float]:
        """
        Get AHN for all the defined points (in RD coordinates). Since many points have to be requested which do not
        necessarily have to be requested in a particular order, we can speed things up by using an asynchronous function.
        As a point is requested, Python does not have to wait to get an answer and can instead issue another request.
        :param points: Points in RD coordinates as e.g. [[1234, 5678], [1239, 5678], ...]
        :param interval:
        :return:
        """
        going_right = points[0][0] <= points[1][0]  # Check in what direction the line goes
        going_up = points[0][1] <= points[1][1]
        map_payload_dict = self._get_map_payload(points, interval)  # Retrieve the compensated map parameters
        width, height = int(map_payload_dict['width']), int(map_payload_dict['height'])
        # Catch ResourceWarnings, raised by suspected non-closure of connections.
        # In reality they *are* closed, yet after a little while.
        # For more information, visit: https://github.com/aio-libs/aiohttp/pull/2045
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            async with aiohttp.ClientSession() as session:  # Start a session
                # Set up an iterator to state in what direction the line should be followed
                i_list = list(range(0, width, 1)) if width > 1 else max(width, height) * [0]
                if not going_right:  # X-axis is positive to the right
                    i_list = i_list[::-1]
                j_list = list(range(0, height, 1)) if height > 1 else max(width, height) * [0]
                if going_up:  # Y-axis is positive downward in images
                    j_list = j_list[::-1]
                i_j_list = list(zip(i_list, j_list))
                tasks = [asyncio.create_task(self._async_get_ahn_of_rd_point(i, j, session, map_payload_dict=map_payload_dict))
                        for i, j in i_j_list]  # Create all the tasks that have to be executed
                ahn_list = await asyncio.gather(*tasks, return_exceptions=False)  # Wait till all tasks are completed
            # Following line can be removed when aiohttp >= 4.0.0 is released
            await asyncio.sleep(0.1)  # Suppresses the last ResourceWarnings https://github.com/aio-libs/aiohttp/issues/1925
        return ahn_list  # Return the AHN values in list format


    async def _async_get_ahn_of_rd_point(self, point_index, point_jndex, session, map_payload_dict) -> float:
        """
        Get AHN of a single point. This is done by composing the request URL from the URL base and the payload
        :param point_index: Which index in i of the points should be retrieved on the bbox
        :param point_jndex: Which index in j of the points should be retrieved on the bbox
        :param session: Session that should be used for the request
        :param map_payload_dict:
        :return: AHN value
        """
        if self.source == AhnSource.DTM:
            bladindex = AhnDTMBladIndex[self.version]
        else:
            bladindex = AhnDSMBladIndex[self.version]

        # Create the payload dict
        payload = {
            "service": "wms",
            "version": "1.3.0",
            "request": "getfeatureinfo",
            "layers": bladindex,
            "format": "image/png",
            "crs": "EPSG:28992",
            "query_layers": bladindex,
            "info_format": "application/json",
            "i": f"{point_index}",
            "j": f"{point_jndex}",
        }
        payload.update(map_payload_dict)

        url_ahn = AhnUrls[self.version]
        async with session.get(url_ahn, params=payload) as response:  # Set up the asynchronous request
            response.raise_for_status()
            json = await response.json()  # Wait for the response to arrive
            ahn = float(json['features'][0]['properties']['GRAY_INDEX'])  # Get AHN from the returned json
            return ahn


