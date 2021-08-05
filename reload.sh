#!/bin/bash
sudo systemctl stop rhasspy.skill.bring.service
sudo systemctl daemon-reload
sudo systemctl start rhasspy.skill.bring.service