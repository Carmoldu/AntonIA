@echo off
poetry run python src/AntonIA/pipeline.py grandma=AntonIA_cat profile=cloud
poetry run python src/AntonIA/pipeline.py grandma=AntonIA_cast profile=cloud
pause