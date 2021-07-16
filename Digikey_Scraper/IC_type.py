

def Find_IC_Type( category_text):
    if 'Clock/Timing - Clock Buffers, Drivers' in category_text:
        return 'CLK Buffer'
    
    elif 'Clock/Timing - Clock Generators, PLLs, Frequency Synthesizers' in category_text:
        return 'PLL'

    elif 'Clock/Timing - Real Time Clocks' in category_text:
        return 'RTC'

    elif 'Data Acquisition - Analog to Digital Converter' in category_text:
        return 'ADC'

    elif 'Data Acquisition - Digital to Analog Converter' in category_text:
        return 'DAC'

    elif 'Embedded - CPLDs' in category_text:
        return 'CPLD'

    elif 'Embedded - FPGAs' in category_text:
        return 'FPGA'

    elif 'Embedded - Microcontrollers' in category_text:
        return 'Microcontroller'

    elif 'Embedded - Microprocessors' in category_text:
        return 'Microprocessor'

    elif 'Embedded - System On Chip' in category_text:
        return 'SOC'

    elif 'Interface - Analog Switches, Multiplexers, Demultiplexers' in category_text:
        return 'Analog Switch, MUX, De-MUX'

    elif 'Interface - CODECs' in category_text:
        return 'CODEC'
    elif 'Interface - Drivers, Receivers, Transceivers' in category_text:
        return 'Driver,Receiver'

    elif 'Interface - UARTs' in category_text:
        return 'UART'

    elif 'Linear - Amplifiers - Instrumentation, OP Amps, Buffer Amps' in category_text:
        return 'Opamp'

    elif 'Video' in category_text:
        return 'Video'

    elif 'Logic - Translators, Level Shifters' in category_text:
        return 'Level Shift'

    elif 'Logic - Universal Bus Functions' in category_text:
        return 'USB'

    elif 'Memory' in category_text:
        return 'Memory'

    elif 'PMIC - Power Over Ethernet' in category_text:
        return 'P.O.E.'

    elif 'PMIC - Voltage Reference' in category_text:
        return 'Voltage Reference'

    elif 'PMIC - Voltage Regulators - DC DC Switching' in category_text:
        return 'DC-DC Conv'

    elif 'PMIC - Voltage Regulators - Linear' in category_text:
        return 'LDO'
    
    elif 'PMIC - Voltage Regulators - Special Purpose' in category_text:
        return 'Voltage Regulator'
    
    elif 'PMIC - Supervisors' in category_text:
        return 'PMIC Supervisor'
    
    elif 'Logic - Buffers, Drivers, Receivers, Transceivers' in category_text:
        return 'Buffers, Drivers, Receivers'
    
    elif 'PMIC - Motor Drivers, Controllers' in category_text:
        return 'Motor Driver'

    elif 'Logic - Gates and Inverters' in category_text:
        return 'Logic Gate'

    elif 'Logic - Signal Switches, Multiplexers, Decoders' in category_text:
        return 'Logic Switch, Mux'

    elif 'PMIC - Power Supply Controllers, Monitors' in category_text:
        return 'Power Supply Monitor'

    elif 'Temperature Sensors' in category_text:
        return 'Temp Sensor'
    
    elif 'Interface - Analog Switches - Special Purpose' in category_text:
        return 'Analog Switch'
    
    elif 'Linear - Comparators' in category_text:
        return 'Comparator'

    elif 'Transistors - FETs, MOSFETs - Arrays' in category_text:
        return 'FET Array'
    
    elif 'Interface - Controllers' in category_text:
        return 'Interface'
    
    elif 'Interface - Serializers, Deserializers' in category_text:
        return 'Serializer/Deserializer'
    
    elif 'Common Mode Chokes' in category_text:
        return 'Common Mode Choke'

    elif 'PMIC' in category_text:
        return 'PMIC'

    elif 'Transistors - Bipolar (BJT) - Single' in category_text:
        return 'BJT'
    
    elif 'Transistors - Bipolar (BJT) - Arrays' in category_text:
        return 'BJT Array'

    elif 'Logic - Flip Flops' in category_text:
        return 'Flip Flop'

    elif 'Optoisolators' in category_text:
        return 'Optoisolator'

    elif 'Embedded - DSP (Digital Signal Processors)' in category_text:
        return 'DSP'
    elif 'Digital Isolators' in category_text:
        return 'Digital Isolator'

    elif 'Interface - Signal Buffers, Repeaters, Splitters' in category_text:
        return 'Signal Buffer'

    elif 'TVS - Thyristors' in category_text:
        return 'TVS'

    elif 'Data Acquisition - Digital Potentiometers' in category_text:
        return 'Digital Pot'

    elif 'Transistors - FETs, MOSFETs - Single' in category_text:
        return 'FET'

    elif 'Interface - Encoders, Decoders, Converters' in category_text:
        return 'Encoder/Decoder'

    elif 'Unclassified' in category_text:
        return 'Unclassified'

    elif 'DC DC Converters' in category_text:
        return 'DC DC Converter'

    elif 'Feed Through Capacitors' in category_text:
        return 'Feed Through Capacitor'

    elif 'Inrush Current Limiters (ICL)' in category_text:
        return 'Inrush Current Limiter'

    elif 'Solid State Relays' in category_text:
        return 'SSR'

    elif 'PTC Resettable Fuses' in category_text:
        return 'PTC Fuse'
    
    elif 'Surge Suppression ICs' in category_text:
        return 'Surge Suppress'

    elif 'Interface - I/O Expanders' in category_text:
        return 'IO Expand'

    elif 'Specialized ICs' in category_text:
        return 'Special'

    elif 'Pulse Transformers' in category_text:
        return 'Pulse Transformer'

    elif 'Interface - Telecom' in category_text:
        return 'Telecom'

    elif 'EMI/RFI Filters (LC, RC Networks)' in category_text:
        return 'EMI Filter'    

    elif 'Clock/Timing' in category_text:
        return 'Clock/Timing'    
        
    elif 'LED Indication - Discrete' in category_text:
        return 'LED'    
        
    elif 'Fuses' in category_text:
        return 'Fuse'    

    elif 'Motion Sensors - Gyroscopes' in category_text:
        return 'Gyro'    

    elif 'Motion Sensors - Accelerometers' in category_text:
        return 'Accelerometer'

    elif 'Linear - Amplifiers' in category_text:
        return 'Amplifier'

    elif 'Interface - Specialized' in category_text:
        return 'Special'

    else:
        return ''

      

    

    

    





    


        


        

    



    

    










        


















    






        
    






















