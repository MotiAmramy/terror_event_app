

def validate_groq_json(groq_json: dict):
        required_fields = ["country", "country_latitude", "country_longitude", "category", "continent"]
        valid = all(groq_json[field] not in [None, 0, ""] for field in required_fields)
        res = {'category': groq_json['category'], 'country': groq_json['country'], 'continent':  groq_json['continent'],
                'country_longitude':  groq_json['country_longitude'],
                'country_latitude': groq_json['country_latitude']}  if valid else None
        return res


