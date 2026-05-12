from langchain.tools import tool
import importlib

@tool
def focus_data(distance: float, xr: int, yr: int, xg: int, yg: int, xb: int, yb: int):
    """
    Create a dataset for the achromatic metalens design task.

    Input:
        distance: Focal length of the achromatic metalens, in micrometer.
        xr: The x-coordinate of the focal point for red light on the focal plane.
        yr: The y-coordinate of the focal point for red light on the focal plane.
        xg: The x-coordinate of the focal point for green light on the focal plane.
        yg: The y-coordinate of the focal point for green light on the focal plane.
        xb: The x-coordinate of the focal point for blue light on the focal plane.
        yb: The y-coordinate of the focal point for blue light on the focal plane.
    """
    module = importlib.import_module("Focus.create_data")
    return module.func(distance, xr, yr, xg, yg, xb, yb)

@tool
def holography_data(distance_min: int, distance_max: int):
    """
    Create a dataset for the Holography task.

    Input:
        distance_min: The shortest focal length from the holography to the metasurface, in micrometer.
        distance_max: The longest focal length from the holography to the metasurface, in micrometer.
    """
    module = importlib.import_module("Holography.create_data")
    return module.func(distance_min, distance_max)

@tool
def generator_data(contimg: str, styleimg: str, distance: int):
    """
    Create a dataset for the image style transfer task.

    Input:
        contimg: The filename of the content image, such as x.png
            Do not include:
                - a leading slash (/x.png)
                - ./x.png
                - any directory path
                - any extra text
        styleimg: The filename of the style image, such as x.png
            Do not include:
                - a leading slash (/x.png)
                - ./x.png
                - any directory path
                - any extra text
        distance: The focal length of the imaging plane to the metasurface, in micrometer.
    """
    module = importlib.import_module("Generator.create_data")
    return module.func(contimg, styleimg, distance)

