<?php
/**
 * Created by PhpStorm.
 * User: CaptainT
 * Date: 2022/4/13
 * Time: 11:18
 */

namespace App\Http\Controllers\Api\user;


use App\Http\Controllers\Controller;
use App\Models\Articel;
use Illuminate\Http\Request;

class IndexController
{
    public function index()
    {
        $article = new Articel();
        $a = Articel::query()->where(['status' => 2])->get();
        return response()->json(['status' => 1, 'msg' => '查询成功！', 'data' => $a]);
    }

    public function listGet()
    {
        $article = new Articel();
        $a = Articel::with(['user'])->where(['status' => 2])->paginate(10);
        return response()->json(['status' => 1, 'msg' => '查询成功！', 'data' => $a]);
    }

    public function detail($id)
    {
        $article = new Articel();
        $a = Articel::query()->where(['status' => 2])->find($id);
        return response()->json(['status' => 1, 'msg' => '查询成功！', 'data' => $a]);
    }

    public function create(Request $request)
    {
        $article = new Articel();
        $user_info = auth()->user();

        $data = $request->all();
        $article->user_id = $user_info['id'];
        $article->title = $data['title'];
        $article->content = $data['content'];
        $article->source = $data['source'];
        $article->save();
        return response()->json(['status' => 1, 'msg' => '提交成功！', 'data' => []]);
    }

    public function edit(Request $request)
    {
        $article = new Articel();

        $data = $request->all();

        $article = Articel::query()->find($data['id']);
        $article->title = $data['title'];
        $article->content = $data['content'];
        $article->source = $data['source'];
        $article->save();
        return response()->json(['status' => 1, 'msg' => '编辑成功！', 'data' => []]);
    }
}