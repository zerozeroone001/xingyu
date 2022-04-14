<?php
/**
 * Created by PhpStorm.
 * User: CaptainT
 * Date: 2022/4/13
 * Time: 11:56
 */

namespace App\Models;


use Illuminate\Database\Eloquent\Model;

class Articel extends Model
{
    protected $table = 'article';
//    protected $connection  = 'users';

    protected $primaryKey = 'id';


    public function user()
    {
        return $this->hasOne('App\Models\User', 'id', 'user_id');
    }
}