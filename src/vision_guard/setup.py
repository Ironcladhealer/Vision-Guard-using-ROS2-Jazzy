from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'vision_guard'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='You',
    maintainer_email='you@example.com',
    description='Vision Guard ROS2 package',
    license='MIT',
    entry_points={
        'console_scripts': [
            'detector_node = vision_guard.detector_node:main',
            'tracker_node = vision_guard.tracker_node:main',
            'response_node = vision_guard.response_node:main',
        ],
    },
)