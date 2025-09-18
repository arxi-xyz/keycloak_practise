<?php

namespace App\Http\Controllers;

abstract class Controller
{
    public function response($data, $msg, $code = 200)
    {
        return response([
            'message' => $msg,
            'data' => $data
        ])->json()->setStatusCode($code);
    }
}
