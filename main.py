import mpl
import ki
import mail
import secret_file

def add_missing_fields(entry):
    entry.in_charge = "John Doe"                    # MOCK
    entry.in_charge_mail = "dbollian@gmail.com"     # MOCK
    entry.ki_response = ki.infer("### Question: "+entry.error_text.replace("\n", " ")+"\n")
    entry.ki_response = entry.ki_response.removeprefix("### Question: "+entry.error_text).strip()
    return entry

def get_message(entry):
    return f"Hello {entry.in_charge},\n\nAn error occured in the integration flow {entry.iflow_name}. (GUID: {entry.message_guid})\n\nError Message:\n{entry.error_text}\n\nKI-generated Advice:\n{entry.ki_response}"
    
def main(start, end):

    host = secret_file.mpl_host
    start = "2024-03-01T00:00:00"
    end = "2024-03-01T00:00:10"

    entries = mpl.get_mpls(host, start, end)
    for entry in entries:
        entry = add_missing_fields(entry)
        message = get_message(entry)
        mail.send_mail(entry.in_charge_mail, message, entry.iflow_name)
        break