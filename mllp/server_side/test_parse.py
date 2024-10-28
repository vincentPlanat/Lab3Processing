import hl7

# Sample HL7 message
message = "MSH|^~\\&|GHH LAB|ELAB-3|GHH OE|BLDG4|200202150930||ORU^R01|CNTRL-3456|P|2.4\r"
message += "PID|||555-44-4444||EVERYWOMAN^EVE^E^^^^L|JONES|196203520|F|||153 FERNWOOD DR.^^STATESVILLE^OH^35292||(206)3345232|(206)752-121||||AC555444444||67-A4335^OH^20030520\r"
message += "OBR|1|845439^GHH OE|1045813^GHH LAB|1554-5^GLUCOSE|||200202150730||||||||555-55-5555^PRIMARY^PATRICIA P^^^^MD^^LEVEL SEVEN HEALTHCARE, INC.|||||||||F||||||444-44-4444^HIPPOCRATES^HOWARD H^^^^MD\r"
message += "OBX|1|SN|1554-5^GLUCOSE^POST 12H CFST:MCNC:PT:SER/PLAS:QN||^182|mg/dl|70_105|H|||F"

print(f'{message}'.replace('\r', '\n'))

# Parse the HL7 message
parsed_message = hl7.parse(message)

# Extracting segments
msh_segment = parsed_message.segment('MSH')
pid_segment = parsed_message.segment('PID')
obr_segment = parsed_message.segment('OBR')
obx_segment = parsed_message.segment('OBX')

# Extracting fields from segments
sending_facility = msh_segment[4][0]
patient_id = pid_segment[3][0]
patient_name = pid_segment[5][0][1]
test_name = obr_segment[4][0][0]
result_value = obx_segment[5][0][1]

print(f"Sending Facility (msh_segment[4][0]): {sending_facility}")
print(f"Patient ID       (pid_segment[3][0]):{patient_id}")
print(f"Patient Name     (pid_segment[5][0][1]): {patient_name}")
print(f"Test Name        (obr_segment[4][0][0]): {test_name}")
print(f"Result Value     (obx_segment[5][0][1]): {result_value}")
