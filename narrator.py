"""
Script that generates short narrations for a minecraft settlement using LLM.
"""
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import re
import json
from gdpc import Block
import glm

# from gdpc import __url__, Editor, Block, geometry, vector_tools, Transform
# from gdpc.vector_tools import Rect, Box


def generate_narrations(building_types, path="narrations.json", n=5):
    """
    Generates n narrations for each building type, postprocesses narrations by ensuring they only
    contain complete sentences that are not repeated, and stores all narrations in a format that
    allows to load them and access them via the building type from another file.

    Args:
        building_types (list): List of building types.
        path (str): Path to store the generated narrations.
        n (int, optional): Number of narrations to generate for each building type and prompt. Defaults to 5.
    """
    # Load pre-trained GPT-2 model and tokenizer
    model_name = "gpt2-large"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    narrations_dict = {}

    for building_type in building_types:
        prompts = [
            f"Welcome to the town's {building_type}! Here, you can",
            f"You entered a {building_type}! This is a place where",
            f"This is a {building_type}! In this {building_type},",
            f"Welcome to our {building_type}! Here, you'll find",
            f"Step inside the {building_type} and discover",
            f"Explore the wonders of the {building_type}! From",
            f"Have you ever been to a {building_type} like this? It offers",
            f"Behold the magnificent {building_type}! It's a haven for",
            f"Immerse yourself in the enchantment of the {building_type} and experience",
            f"Prepare to be amazed by the {building_type}! With its",
        ]
        building_narrations = []

        for prompt in prompts:
            narrations = generate_building_narration(
                model, prompt, tokenizer, building_type, n
            )

            for narration in narrations:
                # Post-process the narration
                sentences = re.split(r"(?<=[.!?])\s+", narration)

                # remove last sentence if it is incomplete
                if not re.search(r"[.!?]$", sentences[-1]):
                    sentences = sentences[:-1]
                print(sentences)

                if len(sentences) > 0:
                    # remove duplicate sentences
                    unique_sentences = [sentences[0]]
                    for sentence in sentences[1:]:
                        if sentence not in unique_sentences and "\n" not in sentence:
                            unique_sentences.append(sentence)

                    sentences = unique_sentences

                    # print(sentences)
                    # print(" ".join(sentences))

                    building_narrations.append(" ".join(sentences))

        narrations_dict[building_type] = list(building_narrations)

    # Store the narrations as JSON
    with open(path, "w") as file:
        json.dump(narrations_dict, file)

    print(f"Narrations generated and saved to {path}.")


def generate_building_narration(model, prompt, tokenizer, building_type, n):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    outputs = model.generate(
        input_ids,
        max_length=50,
        num_return_sequences=n,
        temperature=0.95,
        do_sample=True,
    )
    narrations = [
        tokenizer.decode(output, skip_special_tokens=True) for output in outputs
    ]

    return narrations


def place_narration_block(editor, coordinates, house_type):
    """
    Places a command block at the given coordinates and a pressure plate on top.
    When triggered, the command block sends a a narration to the nearest player.
    The narration is stored in narrations.json and fits the provided house_type.
    """
    with open("narrations.json", "r") as file:
        narrations = json.load(file)

    # Access narrations for building type
    building_narrations = narrations.get(
        house_type, ["No available narration for this building type..."]
    )

    narration = np.random.choice(building_narrations)
    command = "msg @p "
    command = command + narration
    data_string = '{Command: "' + command + '"}'

    editor.placeBlock(coordinates, Block("minecraft:command_block", data=data_string))
    editor.placeBlock(coordinates + glm.ivec3(0, 1, 0), Block("oak_pressure_plate"))


if __name__ == "__main__":
    generate_narrations(
        ["bakery", "church", "school", "villager house", "farm"], "narrations.json", n=3
    )
    # generate_narrations(["bakery"], "narrations.json", n=3)
