# Email Templates for Meeting Scheduling

## Confirmation Template
```
Subject: Meeting Confirmed - {{meeting_title}} on {{date}}

Dear {{recipient_name}},

I'm pleased to confirm our meeting:

**Meeting Details:**
- Title: {{meeting_title}}
- Date & Time: {{meeting_time}} 
- Duration: {{duration}} minutes
- Participants: {{participants}}
- Location/Link: {{location}}

Thank you for your flexibility during the scheduling process. Looking forward to our productive discussion.

Best regards,
Scheduling Assistant
```

## Reschedule Request Template
```
Subject: Request to Reschedule - {{meeting_title}}

Dear {{recipient_name}},

I need to request a reschedule for our upcoming meeting "{{meeting_title}}" originally planned for {{original_time}}.

{{reason}}

I apologize for any inconvenience this may cause. Here are some alternative times that would work:

{{alternative_times}}

Please let me know which option works best for you, or feel free to suggest other times.

Thank you for your understanding.

Best regards,
Scheduling Assistant
```

## Apology + Alternative Template  
```
Subject: Apology and Alternative Options - {{meeting_title}}

Dear {{recipient_name}},

I sincerely apologize for the scheduling conflict with our meeting "{{meeting_title}}". 

{{explanation}}

To resolve this, I'd like to propose the following alternatives:

{{alternatives}}

I'm committed to finding a time that works for everyone. Please let me know your preference, or if you'd like to suggest different options.

Thank you for your patience and flexibility.

Best regards,
Scheduling Assistant
```

## Counter-Proposal Template
```
Subject: Alternative Time Proposal - {{meeting_title}}

Dear {{recipient_name}},

Thank you for proposing {{original_time}} for our meeting "{{meeting_title}}".

{{constraint_explanation}}

I'd like to suggest the following alternative times that would work better:

{{counter_proposals}}

I believe these options will allow for better participation and productivity. Please let me know which works best for you.

Looking forward to our meeting.

Best regards,
Scheduling Assistant
```

## Decline Template
```
Subject: Unable to Schedule - {{meeting_title}}

Dear {{recipient_name}},

Thank you for the meeting request for "{{meeting_title}}".

Unfortunately, I'm unable to attend due to {{reason}}.

{{alternatives_suggestion}}

I appreciate your understanding and hope we can connect in an alternative way.

Best regards,
Scheduling Assistant
```

## Negotiation Summary Template
```
Subject: Meeting Scheduled Successfully - {{meeting_title}}

Dear Team,

After our collaborative scheduling process, I'm pleased to confirm that we've successfully scheduled our meeting:

**Final Meeting Details:**
- Title: {{meeting_title}}
- Date & Time: {{final_time}}
- Duration: {{duration}} minutes
- Participants: {{all_participants}}

**Scheduling Summary:**
- Negotiation rounds: {{rounds}}
- Final consensus reached
- All participant preferences considered

Thank you all for your flexibility and collaboration in making this meeting possible.

Calendar invitations will follow shortly.

Best regards,
Scheduling Assistant
```