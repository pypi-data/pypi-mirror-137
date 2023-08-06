import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymqttusb", # Replace with your own username
    version="1.1.3",
    author="Didier Orlandi",
    author_email="didier.orlandi@wanadoo.fr",
    description="Connexion USB <-> MQTT ssl ou wss",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=[
          'paho-mqtt',
          'mqtt_thread',
          'pyserial>=3.5',
      ],
)