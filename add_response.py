import mpl
import ki

entries = mpl.get_mpls()

for entry in entries:
    entry.in_charge = "John Doe"
    entry.ki_response = ki.infer("### Question: "+entry.error_text)
    entry.ki_response = entry.ki_response.removeprefix("### Question: "+entry.error_text).strip()
    message = f"Hello {entry.in_charge},\n\nAn error occured in the integration flow {entry.iflow_name}. (GUID: {entry.message_guid})\n\nError Message:\n{entry.error_text}\n\nKI-generated Advice:\n{entry.ki_response}"
    print(message+"\n\n")