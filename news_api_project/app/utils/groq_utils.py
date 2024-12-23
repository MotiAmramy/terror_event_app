





def validate_groq_json(groq_json: dict):
    required_fields = ["country", "country_latitude", "country_longitude", "category"]

    valid = all(groq_json[field] not in [None, 0, ""] for field in required_fields)

    return {'category': groq_json['category'], 'country': groq_json['country'],
            'city':  groq_json['city'], 'continent':  groq_json['continent'],
            'country_longitude':  groq_json['country_longitude'],
            'country_latitude': groq_json['country_latitude']}  if valid else None




