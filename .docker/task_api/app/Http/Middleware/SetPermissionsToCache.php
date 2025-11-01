<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Redis;
use Illuminate\Validation\UnauthorizedException;
use Symfony\Component\HttpFoundation\Response;

class SetPermissionsToCache
{
    /**
     * Handle an incoming request.
     *
     * @param \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response) $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $url = config('keycloak.authz.base_url') . '/realms/' . config('keycloak.authz.realm_name') . '/protocol/openid-connect/token';

        $response = Http::asForm()
                        ->withHeaders([
                            'Authorization' => \request()->header('Authorization'),
                        ])
                        ->post($url, [
                            'grant_type'    => 'urn:ietf:params:oauth:grant-type:uma-ticket',
                            'audience'      => config('keycloak.authz.client_id'),
                            'response_mode' => 'permissions',
                        ]);

        if ($response->failed()) {
            throw new UnauthorizedException('unauthorized');
        }

        $permissions = [];

        foreach ($response->json() as $item) {
            $rsname = $item['rsname'] . '_';
            foreach ($item['scopes'] ?? [] as $scope) {
                $permissions[] = $rsname . $scope;
            }
        }

        $userId = $request->header('X-Forwarded-UserId');

        Redis::setex(
            "permissions:user:$userId",
            1800,
            json_encode($permissions, JSON_UNESCAPED_UNICODE)
        );

        return $next($request);

    }
}
