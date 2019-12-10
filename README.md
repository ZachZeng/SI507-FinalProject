# Data Source

## Game data source
(scraping from) https://www.igdb.com/discover + (API call) https://rawg.io/apidocs

## Platform data source
(API call) https://rawg.io/apidocs

# Code Structure

## File Structure
	final_project (virtual environment)
	templates/
		index.html
	static/
		style.css
	requirements.txt
	app.py
	model.py
	final_pro_test.py
	store_data.py
	README.md

## Key data processing functions
	get_platform_percentage()
	get_platform_ratings()
	get_platform_top()
	get_game_detail()


## Class
Game
	name
	release date
	description
	platform

## List
	game_detail_result
	top_platform_game_result


# User Guide

Environment requirements: requirements.txt

Get Data and Build Database

	python store_data.py

Run Flask APP

	python app.py

Open localhost:5000
Page include:
	Two data visulization
	One form to search platform top game
	One form to search game detail

