_CONTENT = {
	'.gitlab-ci.yml': '''stages:
- check
- deploy

image: {{ base_image }}

services:
  - postgres:13.1-alpine

variables:
  DJANGO_DATABASE_URL: pgsql://postgres:@postgres/postgres
  DJANGO_SECRET_KEY: 'static'
  DJANGO_ALLOWED_HOSTS: '127.0.0.1,localhost'
  ### CI database configuration
  POSTGRES_HOST_AUTH_METHOD: trust
  #POSTGRES_DB: nice_marmot
  #POSTGRES_USER: runner
  POSTGRES_PASSWORD: ""
  ### CI configuration
  # Change pip's cache directory to be inside the project directory since we can
  # only cache local items.
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  # Faster CI caching
  FF_USE_FASTZIP: 1

cache:
  paths:
    - venv/
    - .cache/pip
    - .cache/pypoetry
    # This caching scheme is somewhat aggressive because
    # it caches poetry virtualenv. This is faster but can
    # potentially result in not-completely-clean builds
    # if there's a bug in poetry --sync.
    # For less aggressive caching, use this instead:
    #- .cache/pypoetry/artifacts
    #- .cache/pypoetry/cache

before_script:
  - python -V  # Print out python version for debugging
  - pip install -q poetry==1.7.1
  - poetry config cache-dir "$CI_PROJECT_DIR/.cache/pypoetry"
  - poetry config virtualenvs.create true
  - poetry self add poetry-plugin-export || true

test:
  stage: check
  script:
    - script/setup
    - script/cibuild
  coverage: '/^TOTAL.+?(\d+\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

deploy_bleeding:
  when: manual
  stage: deploy
  image: "docker:19.03.1"
  before_script:
    - docker info
  services: []
  cache: {}
  script:
    - echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin {% if repository %}{{ repository }}{% endif %}
    - script/x-dockerbuild -t bleeding
    - script/x-dockerpush -t bleeding
# environment:
#   name: production
#   url: https://mywebsite.com

deploy_main:
  when: manual
  stage: deploy
  image: "docker:19.03.1"
  before_script:
    - docker info
  services: []
  cache: {}
  script:
    - echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin {% if repository %}{{ repository }}{% endif %}
    - script/x-dockerbuild
    - script/x-dockerpush
# environment:
#   name: production
#   url: https://mywebsite.com

# ISSUE: nobody can guarantee that image did not change between deploy_bleeding and deploy_promote. Use at your own risk.
# deploy_promote:
#   when: manual
#   stage: deploy
#   script:
#     - docker tag '{{ repository }}{% if repository %}/{% endif %}{{ image }}:bleeding' '{{ repository }}{% if repository %}/{% endif %}{{ image }}'
#     - docker push '{{ repository }}{% if repository %}/{% endif %}{{ image }}'


# pages:
#   script:
#     - pip install sphinx sphinx-rtd-theme
#     - cd doc ; make html
#     - mv build/html/ ../public/
#   artifacts:
#     paths:
#       - public
#   only:
#     - master
'''
}
