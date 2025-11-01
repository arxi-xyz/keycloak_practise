<?php

namespace App\Policies;

use App\Enums\PermissionEnum;
use App\Models\User;
use App\Models\Task;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Redis;

class TaskPolicy
{
    public function viewAny(?User $user): bool
    {
        return $this->hasPermission(PermissionEnum::TASK_INDEX->value);
    }

    public function view(?User $user, Task $task): bool
    {
        return $this->hasPermission(PermissionEnum::TASK_INDEX->value);
    }

    public function create(?User $user): bool
    {
        return $this->hasPermission(PermissionEnum::TASK_STORE->value);
    }

    public function update(?User $user, Task $task): bool
    {
        return $this->hasPermission(PermissionEnum::TASK_UPDATE->value);
    }

    public function delete(?User $user, Task $task): bool
    {
        return $this->hasPermission(PermissionEnum::TASK_DELETE->value);
    }

    protected function hasPermission(string $permission): bool
    {
        $user_id = request()->header('X-Forwarded-UserId');
        $permissions = Redis::get("permissions:user:{$user_id}");

        if (!$permissions) {
            return false;
        }

        $permissions = json_decode($permissions, true);
        Log::info("Permissions:", $permissions);
        Log::info("comparison:", [$permission, $permissions]);

        return in_array($permission, $permissions ?? []);
    }
}
