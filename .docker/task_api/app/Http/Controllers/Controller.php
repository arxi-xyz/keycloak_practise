<?php

namespace App\Http\Controllers;

use Illuminate\Foundation\Auth\Access\AuthorizesRequests;

abstract class Controller extends \Illuminate\Routing\Controller
{
    use AuthorizesRequests;
    public function response($data, $msg, $code = 200)
    {
        return response()->json([
            'message' => $msg,
            'data' => $data
        ])->setStatusCode($code);
    }
}
