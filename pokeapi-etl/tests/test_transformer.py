from etl.transform.transformer import transform_pokemon_data

def test_transform_pokemon_data():
    raw_data = {
        'pokemon': {
            'id': 1,
            'name': 'bulbasaur',
            'height': 7,
            'weight': 69,
            'base_experience': 64,
            'is_default': True,
            'types': [{'slot': 1, 'type': {'name': 'grass'}}],
            'abilities': [{'ability': {'name': 'overgrow'}, 'is_hidden': False}],
            'stats': [{'stat': {'name': 'hp'}, 'base_stat': 45, 'effort': 0}]
        }
    }
    
    result = transform_pokemon_data(raw_data)
    
    assert result['pokemon']['name'] == 'bulbasaur'
    assert result['types'][0]['type_name'] == 'grass'
    assert result['abilities'][0]['ability_name'] == 'overgrow'
    assert result['stats'][0]['stat_name'] == 'hp'