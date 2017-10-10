#!/bin/bash

ps -ef|grep appium | grep -v grep|awk '{print $2}' | xargs kill -9
