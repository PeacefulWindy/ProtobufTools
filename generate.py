import os
import json
import shutil

def move(fromPath,toPath):
    if not os.path.exists(toPath):
        os.makedirs(toPath)
    
    shutil.copytree(fromPath, toPath,dirs_exist_ok=True)

def generate(inputPath,outputPath):
    files=os.listdir(inputPath)
    for it in files:
        if not it.find(".proto"):
            continue
        
        pbFileName=it.replace(".proto",".pb")

        inputProto=os.path.join(inputPath,it)
        outputProto=os.path.join(outputPath,pbFileName)
        
        cmd="protoc --descriptor_set_out="+outputProto+" --include_imports --proto_path="+inputPath+" "+inputProto
        os.system(cmd)
        print(inputProto,"=>",outputProto)

def main():
    json_data={}
    with open("../config.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    generate(json_data["input"],json_data["output"])

    print("will move proto...")

    if json_data["move"]:
        if json_data["move"]["client"]:
            print("move client proto...")
            move(json_data["output"],json_data["move"]["client"])

        if json_data["move"]["server"]:
            print("move server proto...")
            move(json_data["output"],json_data["move"]["server"])
        print("move proto finish!")
    print()

main()