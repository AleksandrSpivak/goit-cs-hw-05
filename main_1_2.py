# reading and coping files done by the same function

import argparse
import logging
import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile


parser = argparse.ArgumentParser(description="Sorting files")
parser.add_argument("--source", "-s", required=True, help="Source directory")
parser.add_argument("--output", "-o", help="Output directory", default="destination")

args = vars(parser.parse_args())
source = AsyncPath(args["source"])
output = AsyncPath(args["output"])

file_number = 0


async def read_folder(path: AsyncPath, output: AsyncPath):
    """
    Asynchronously reads the contents of the specified folder and copies all files to the specified output folder.
    Takes the 'path' parameter as the source folder and the 'output' parameter as the destination folder.
    Increments the global 'file_number' for each file copied.
    """
    global file_number

    async for child in path.iterdir():

        if await child.is_dir():
            await read_folder(child, output)

        elif await child.is_file():
            folder = AsyncPath(output / child.suffix[1:])
            try:
                await folder.mkdir(exist_ok=True, parents=True)
                await copyfile(child, folder / child.name)
                file_number += 1
            except OSError as err:
                logging.error(err)
    return


async def main():
    await asyncio.gather(read_folder(source, output))


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    asyncio.run(main())

    print(f"{file_number} files were copied from '{source}' directory to '{output}' directory")
