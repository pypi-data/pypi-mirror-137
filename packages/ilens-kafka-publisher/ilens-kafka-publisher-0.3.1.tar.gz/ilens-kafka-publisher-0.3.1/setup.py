from setuptools import setup

setup(
    name='ilens-kafka-publisher',
    version='0.3.1',
    packages=['ilens_kafka_publisher'],
    url='https://unifytwin.com',
    license='Restricted',
    author='Charan',
    author_email='charankumar@knowledgelens.com',
    description='Utility for Publishing messages to Kafka in iLens',
    install_requires=[
          "kafka-python~=2.0.2"
      ],
)
