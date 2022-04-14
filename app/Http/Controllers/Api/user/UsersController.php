<?php
/**
 * Created by PhpStorm.
 * User: CaptainT
 * Date: 2022/4/14
 * Time: 16:25
 */

namespace App\Http\Controllers\Api\user;


use App\Http\Controllers\Controller;

class UsersController extends Controller
{

    public function __construct()
    {
        $this->middleware('jwt.auth', ['except' => ['login']]);
        // 另外关于上面的中间件，官方文档写的是『auth:api』
        // 但是我推荐用 『jwt.auth』，效果是一样的，但是有更加丰富的报错信息返回
    }

    public function login()
    {
        $credentials = request(['mobile', 'password']);

        if (! $token = auth('api')->attempt($credentials,true)) {
            return response()->json(['error' => '账号密码错误'], 401);
        }
        return $this->respondWithToken($token);
    }


    public function logout()
    {
        auth('api')->logout();

        return response()->json(['message' => '退出成功！']);
    }


    public function refresh()
    {
        return $this->respondWithToken(auth('api')->refresh());
    }


    protected function respondWithToken($token)
    {
        return response()->json([
            'access_token' => $token,
            'token_type' => 'bearer',
        ]);
    }

}