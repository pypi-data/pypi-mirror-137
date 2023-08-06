import streamlit as st
from pollination_streamlit_io import inputs

# get the platform from the query uri
query = st.experimental_get_query_params()
platform = query['__platform__'][0] if '__platform__' in query else 'web'

if platform == 'Rhino':
    st.subheader('GDI Bug test')

    def calc():
        id = 10
        while id < 60:
            id+=1
            legend = {
            'type': 'LegendScreen',
            'x': '50',
            'y': '50',
            'height': '500',
            'width': id,
            'min': 0,
            'max': 100,
            'num': 8,
            'font': 17,
            'colors': [{'r': '255', 'g': '0', 'b': '0' },
                {'r': '0', 'g': '255', 'b': '255' }, 
                {'r': '12', 'g': '123', 'b': '255' }, 
                {'r': '0', 'g': '255', 'b': '0' }]
            }
            inputs.send(data=legend,
            label='GO!',
            defaultChecked=True,
            uniqueId='unique-id-02' + str(id), 
            options={'layer':'StreamlitLayer'}, 
            key='pollination-inputs-send-02' + str(id))

    if st.button('CLick here'):
        calc()

