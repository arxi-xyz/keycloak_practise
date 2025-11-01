<?php

namespace App\Enums;

enum PermissionEnum: string
{
    case TASK_STORE = "task_store";
    case TASK_INDEX = "task_index";
    case TASK_UPDATE = "task_update";
    case TASK_DELETE = "task_delete";
}
