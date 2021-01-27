# UCD Major Planner Scraper

This is a scraper for a potential major planner for UC Davis.

In its current form, it latches on to the myDegree api to get data about major requirements. To do this, it needs what's called a bearer token. Ask Tim how to get your bearer token, and once you do get it, you want to put it a file called 'bearer.token' in the uppermost directory.

Here's a screenshot of where it is if you can decipher it: https://imgur.com/qNK8B9q
There is some sort of experation period for the token so you will have to get a new one if the current one no longer works.

Currently all the script does is output only the major requirements of a desired major in addition to prerequisites for each class. This does not include GE or college requirements. To specify a major, use its code as the first and only argument upon running the script. A list of majors and their codes can be found in `listofmajors.txt`. If a major is not specified, it will default to CS.

Output is directed both to the terminal and to a json file in `output/`.