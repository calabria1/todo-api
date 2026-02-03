from __future__ import annotations

class TaskStatus:
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"

ALLOWED_STATUS = {TaskStatus.PENDENTE, TaskStatus.EM_ANDAMENTO, TaskStatus.CONCLUIDA}
