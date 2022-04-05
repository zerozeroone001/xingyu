<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class IndexController extends Controller
{
    public function index(){
        return response()->json(['status'=>1,'msg'=>'查询成功！','data'=>'hello word']);
    }
}
