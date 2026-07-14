# 09 ai agenten – Block 8

## Beschreibung

\subsection{Code-Review-Agent}
Ein SaaS-Unternehmen nutzt einen Multi-Agent-Workflow für automatische Code-Reviews:

## Verbatim

```
   [PR geoeffnet] -> [Supervisor]
                       |
           +-----------+-----------+
           |           |           |
       [Security]  [Quality]  [Performance]
           |           |           |
           +-----------+-----------+
                       |
                   [Reviewer]
                       |
                   [Feedback im PR]
```
