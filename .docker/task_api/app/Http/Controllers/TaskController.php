<?php

namespace App\Http\Controllers;

use App\Http\Requests\Task\StoreTaskRequest;
use App\Http\Requests\Task\UpdateTaskRequest;
use App\Http\Resources\Task\IndexTaskResource;
use App\Http\Resources\Task\ShowTaskResource;
use App\Models\Task;

class TaskController extends Controller
{
    public function index()
    {
        $tasks = Task::paginate(15);

        return $this->response(
            IndexTaskResource::collection($tasks),
            'index tasks'
        );
    }

    public function show($id)
    {
        return $this->response(
            ShowTaskResource::make(Task::find($id)),
            'show task'
        );
    }

    public function store(StoreTaskRequest $request)
    {
        $user_id = 1; // todo: get user id from keycloak

        $task = Task::create([
            'name' => $request->name,
            'status' => $request->status,
            'user_id' => $user_id,
        ]);
        return $this->response(
            ShowTaskResource::make($task),
            'task created successfully'
        );
    }

    public function update(UpdateTaskRequest $request, $id)
    {
        $task = Task::find($id)->first();
        $user_id = 1;
        $task->update([
            'name' => $request->name,
            'status' => $request->status,
            'user_id' => $user_id,
        ]);

        return $this->response(
            ShowTaskResource::make($task),
            'task updated successfully'
        );
    }

    public function delete($id)
    {
        $task = Task::find($id)->firstOrFail();
        return $this->response([], 'task deleted successfully');
    }
}