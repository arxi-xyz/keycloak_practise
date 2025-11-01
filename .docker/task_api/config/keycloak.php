<?php

use Illuminate\Support\Str;

return [
    'auth' => [
        'client_id' => env('KEYCLOAK_CLIENT_ID', 'client_id'),
        'base_url' => env('KEYCLOAK_BASE_URL', 'http://keycloak.com/'),
        'realm_name' => env('KEYCLOAK_REALM', 'realm')
    ],
    'authz' => [
        'client_id' => env('AUTHZ_CLIENT_ID', 'client_id'),
        'base_url' => env('AUTHZ_BASE_URL', 'http://keycloak.com/'),
        'realm_name' => env('AUTHZ_REALM', 'realm')
    ]
];
