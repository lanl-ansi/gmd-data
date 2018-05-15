from magneto_api.queries import SchemaDescription

if __name__=='__main__':
    schema = SchemaDescription()
    print('Magneto Schema:')
    print('Table: stations:')
    print('Fields:')
    for k in schema.station_fields:
        print('  '+k+': '+schema.station_fields[k])
    print('Table: measurements:')
    print('Fields:')
    for k in schema.measurement_fields:
        print('  '+k+': '+schema.measurement_fields[k])
