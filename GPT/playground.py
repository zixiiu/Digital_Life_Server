from revChatGPT.V1 import Chatbot

chatbot = Chatbot(config={
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJmYXpua3lAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItSWdrRGVKTjN3S2Nhdlp5UmFIdjRzaGhLIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzhkODMxMjJiMWM2ZDQ3YjdhZDFjYmIiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjgxODEyNDYyLCJleHAiOjE2ODMwMjIwNjIsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb2ZmbGluZV9hY2Nlc3MifQ.DGjcPedr2ZhLWciJccX0qcMrWNUxUGbVvyXuyJPctiOIfDE-wDcnRcYCOaUsddsdNeGniEav3NDaatpe7fq4Y2Wz0Wf1tAEXzSEsVGlR4a1Xw6eESianbX_vAQWhkFCkIr2_ryhsdjuoq64f1qPIfJK4zn2UEENDowH-hrzolEc6ApM7j56U1M_mvGozMyYWSP2eFdHsz7FYZBHAhnNfJICv2v8S91wccIRYofpwDv2I6-LnczC-JBWsmpiTx4DKm3xgQTN7f7r0Bs-5b3q6Fgkzo3GeC7BUyM4MmmEB6C_TX1DG77042R_K12tKuRbxv2W-0ykPUOk7pVcXsYBDvg",
    "paid": True,
    "model": "gpt-4",
    "proxy": "127.0.0.1:7890"
})

print("Chatbot: ")
prev_text = ""
complete_text = ""
for data in chatbot.ask(
        "你现在要回复我一段中文的文字，这段文字需要超过两句话。回复中必须用中文标点。",
):
    message = data["message"][len(prev_text):]
    print(message, end="", flush=True)
    if "。" in message or "！" in message or "？" in message:
        print('')
        # print(complete_text)
        complete_text = ""
    else:
        complete_text += message
    prev_text = data["message"]
print()
