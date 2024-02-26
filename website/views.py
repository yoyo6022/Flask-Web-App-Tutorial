from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Pet, User
from . import db
import json
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.environ.get("OPENAI_API_KEY")

views = Blueprint('views', __name__)

def generate_pet_description(pet_name, pet_breed, pet_sex, pet_age, spayed_neutered, personality_description, other_info):
    client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key,
)
    """
    Generates an engaging animal personality description using the OpenAI API, including the pet's name.
    The description will be 200 ~ 300 words long.
    Ensure to present even the more challenging aspects of their personalities in a positive and attractive manner to prospective adopters.
    """
    conversation = [
        {"role": "system", "content": "You are a helpful assistant that generates engaging and detailed pet descriptions."},
        {"role": "user", "content": f"Generate an engaging description for a pet named {pet_name} with the following details: Breed: {pet_breed}, Age: {pet_age}, Sex: {pet_sex}, Spayed/Neutered: {spayed_neutered}, Personality: {personality_description}, Preference: {other_info}."}
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Make sure to use the appropriate model
        messages=conversation
    )
    
    # Extracting the generated description from the response
    if response.choices:
        last_message = response.choices[-1]  # Get the last message from the choices
        description = last_message.message.content  # Access the 'content' attribute of the message
    else:
        description = "Failed to generate description."
    
    return description.strip()



@views.route('/submit-pet', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        pet_name = request.form.get('petName')
        pet_breed = request.form.get('petBreed')
        pet_sex = request.form.get('petSex')
        pet_age = request.form.get('petAge') + ' ' + request.form.get('ageUnit')
        spayed_neutered = request.form.get('spayedNeutered')
        personality_description = request.form.get('petDescription')
        other_info = request.form.get('otherInfo')

         # Generate the pet description using OpenAI's LLM
        pet_description = generate_pet_description(pet_name, pet_breed, pet_sex, pet_age, spayed_neutered, personality_description, other_info)
        # Store the generated description in the database
        new_pet = Pet(name=pet_name, breed=pet_breed, sex=pet_sex, age=pet_age, spayed_neutered=spayed_neutered, other_info=other_info, personality_description=pet_description, user_id=current_user.id)
        db.session.add(new_pet)
        db.session.commit()
        flash('Pet added!', category='success')

    return render_template("home.html", user=current_user)