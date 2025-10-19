<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Task>
 */
class TaskFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public $status = [
        'DONE',
        'PENDING',
        'DOING'
    ];
    public function definition(): array
    {
        return [
            'name' => $this->faker->name,
            'status' => $this->status[rand(0,2)],
            'user_id' => 1
        ];
    }
}