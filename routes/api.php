<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\user\IndexController;
use App\Http\Controllers\Api\user\UsersController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

// 需要登陆的路由

Route::middleware('jwt.auth::api')->group(function(){  //控制器中也有鉴权

    Route::get('/user/create', [IndexController::class,'create']);
    Route::get('/user/edit', [IndexController::class,'edit']);
});

//用户端
Route::get('/user/login', [UsersController::class,'login']);


Route::get('/user/listGet', [IndexController::class,'listGet']);
Route::get('/user/detail/{id}', [IndexController::class,'detail']);
Route::get('/user/index', [IndexController::class,'index']);

