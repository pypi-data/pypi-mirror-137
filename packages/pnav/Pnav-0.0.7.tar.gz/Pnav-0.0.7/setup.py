import setuptools

setuptools.setup(
    name='Pnav',
    version='0.0.7',
    author='Zander Navratil; Z_Nav',
    description='Package with classes I use often in projects. It contains many personal projects and things that may be useful in rare cases.',
    packages=['pnav'],
    long_description='Contains:\ncharCheck:\t\tthis lets you see if a string or element is in a text file\ndateCalc:\t\tcalculates how far away a date is, future or past.\ncandyTimer:\t\tcreates a windows popup that allows you ration candy or food in set intervals with a gui.\nstockScraper:\t\tscrapes the robinhood website for current stock prices and data.\palindrome:\t\tchecks to see if a string is a palindrome.'
)
