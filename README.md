## python-pandas-etl-aws

#### Python ETL using pandas library with AWS S3 & Batch architecture

#### This api uses 3-layer Python

### This app uses conventional commits

[Conventional commits url](https://www.conventionalcommits.org/en/v1.0.0/)

### Docker usage

    Build server
        docker-compose -p python-pandas-etl-aws
    
    Start server
        docker-compose up -d

    Stop server
        docker-compose down

### Standalone usage

    uvicorn app.main:app --reload

### Poetry usage

    Add a new dependency
        poetry add dependency_name / poetry add [dependecy]

    Remove a dependency
        poetry remove dependency_name / poetry remove [dependecy]

    Install all dependencies in pyproject.toml
        poetry install

    To export dependecies into requirements.txt
        poetry export --without-hashes --format=requirements.txt > requirements.txt

### Testing

    To run unit testing
        python -m pytest app/tests/

    To run unit testing coverage
        python -m pytest --cov app/tests/

### Environment variables

To modify/add configuration via environment variables, use the `.env` file, which contains basic app configuration.