<?php

namespace App\Http\Middleware;

use Closure;
use Firebase\JWT\JWK;
use Firebase\JWT\JWT;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Redis;
use Symfony\Component\HttpFoundation\Response;

class KeycloakAuthMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response) $next
     */
    public function handle(Request $request, Closure $next)
    {
        $authHeader = $request->header('Authorization');

        if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }

        $token = substr($authHeader, 7);

        try {
            $jwks = Cache::remember('keycloak_jwks', 3600, function () {
                $url = config('keycloak.base_url') . '/realms/' . config('keycloak.realm_name') . '/protocol/openid-connect/certs';
                $jwks = file_get_contents($url);
                return json_decode($jwks, true);
            });

            $keys = JWK::parseKeySet($jwks);
            $decoded = JWT::decode($token, $keys);

            if (!in_array(config('keycloak.client_id'), (array)$decoded->aud)) {
                return response()->json(['error' => 'Unauthorized'], 401);
            }

            $request->attributes->add(['user' => $decoded]);

        } catch (\Exception $e) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }

        return $next($request);
    }

}
