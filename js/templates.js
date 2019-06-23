// 坑爹的js把format删掉了，我给他手写一个
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length > 0) {    
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                if(args[key]!=undefined){
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
            }
        }
        else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] != undefined) {
                    var reg= new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
    }
    return result;
}

var markColours = // 数字与颜色的对应关系
{
    '0':'lightgray',
    '1':'red',
    '2':'yellow',
    '3':'blue',
    '4':'blueviolet',
    '5':'orange',
    '6':'teal',
    '7':'lime',
}

var dttLocale = // datatable的本地化
{
    language: {
        "sProcessing": "处理中...",
        "sLengthMenu": "每页显示 _MENU_ 篇文献",
        "sZeroRecords": "没有匹配的文献。",
        "sInfo": "显示第 _START_ 至 _END_ 篇文献，共 _TOTAL_ 项",
        "sInfoEmpty": "没有文献可供显示。",
        "sInfoFiltered": "(由 _MAX_ 篇文献过滤)",
        "sInfoPostFix": "",
        "sSearch": "搜索:",
        "sUrl": "",
        "sEmptyTable": "该分类下没有文献。<br>您可以拖动文献至此来上传到此分类。<br>",
        "sLoadingRecords": "载入中...",
        "sInfoThousands": ",",
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": "上页",
            "sNext": "下页",
            "sLast": "末页"
        },
        "oAria": {
            "sSortAscending": ": 以升序排列此列",
            "sSortDescending": ": 以降序排列此列"
        }
    }
};

var _Mlib = // 分类的DOM模板
'<li class="waves-effect list-group-item d-flex \
    justify-content-between align-items-center" lid="{lib_id}" ltype="{type}" \
    ondragover="allowDrop(this, event)" ondragleave="docOut(this);" \
    ondrop="receiveDoc(this, event);" onclick="showDocsIn(this);">\
        {lib_name}\
    <span class="badge badge-primary badge-pill">{doc_count}</span>\
    <button type="button" class="btn btn-outline-danger waves-effect px-1 py-0 m-0 mr-1 mt-1" \
    onclick="delLib(this);"\
    data-toggle="tooltip" title="移除此分类" style="display: none;">\
    <i class="fas fa-trash"></i>\
    </button>\
</li>';

var _Mlib_0 = // 特殊分类（待读）的DOM模板
'<li class="waves-effect list-group-item d-flex \
    justify-content-between align-items-center" lid="{lib_id}" ltype="{type}" \
    ondragover="allowDrop(this, event)" ondragleave="docOut(this);" \
    ondrop="receiveDoc(this, event);" onclick="showDocsIn(this);">\
        {lib_name}\
    <span class="badge badge-primary badge-pill">{doc_count}</span>\
</li>';

var _Mlib_1 = // 特殊分类（全部）的DOM模板（不能拖入文件）
'<li class="waves-effect list-group-item d-flex \
    justify-content-between align-items-center" lid="{lib_id}" ltype="{type}" \
    onclick="showDocsIn(this);">\
        {lib_name}\
    <span class="badge badge-primary badge-pill">{doc_count}</span>\
</li>';

var _Mdoc = // 文章列表的DOM模板
'<tr did="{document_id}">\
    <td class="waves-effect" onclick="changeMark(this);">\
    <div onmousemove="border(this);" onmouseout="deborder(this);" \
    style="width:20px;height:20px;border-radius:50%;background-color:{mark};">\
    </div></td>\
    <td class="waves-effect" data-toggle="tooltip" title="点击以阅读" \
    ondragstart="dragDoc(this, event);" ondragend="dragDocOk(event);" \
    draggable="true" style="min-width:400px;" onclick="readDoc(this);">{title}</td>\
    <td>{fst_author}</td>\
    <td>{source}</td>\
    <td>{year}</td>\
    <td><div class="row m-0 p-0 align-middle" style="width: 128px;">\
        <button type="button" class="btn btn-outline-primary waves-effect px-1 py-0 m-0 mr-1 mt-1" \
        onclick="showinfo(this);" data-toggle="tooltip" title="信息">\
        <i class="fas fa-info-circle"></i>\
        </button>\
        <button type="button" class="btn btn-outline-secondary waves-effect px-1 py-0 m-0 mr-1 mt-1" \
        onclick="addToReadLater(this);" data-toggle="tooltip" title="待读">\
        <i class="fas fa-flag"></i>\
        </button>\
        <button type="button" class="btn btn-outline-info waves-effect px-1 py-0 m-0 mr-1 mt-1" \
        onclick="down(this);" data-toggle="tooltip" title="下载">\
        <i class="fas fa-arrow-down"></i>\
        </button>\
        {remove_btn}\
    </div></td>\
</tr>';

var _MRemoveDoc = // 移除文献的按钮，在'所有文献'中不应该出现
'<button type="button" class="btn btn-outline-default waves-effect px-1 py-0 m-0 mr-1 mt-1" \
    onclick="remFromLib(this);" data-toggle="tooltip" title="从分类中移除">\
    <i class="fas fa-trash"></i>\
</button>';

var _Minfo = // 详细信息的模板
'<h4 did="{document_id}">标题</h4>\
<div class="waves-effect" onclick="editInfo(this)">{title}</div>\
<input id="etitle" value="{title}" type="text" class="form-control" style="display: none">\
<h4>作者</h4>\
<div class="waves-effect" onclick="editInfo(this)">{author_parsed}</div>\
<input id="eauthors" value="{author}" type="text" class="form-control" style="display: none">\
<h4>年份</h4>\
<div class="waves-effect" onclick="editInfo(this)">{year}</div>\
<input id="eyear" onkeydown="return false;" max="9999" min="1" value="{year}" type="number" class="form-control" style="display: none">\
<h4>主题</h4>\
<div class="waves-effect" onclick="editInfo(this)">\
  {topic_parsed}\
</div>\
<input id="ethemes" value="{topic_s}" type="text" class="form-control" style="display: none">\
<h4>来源</h4>\
<div class="waves-effect" onclick="editInfo(this)">{source}</div>\
<input id="esource" value="{source}" type="text" class="form-control" style="display: none">\
<h4>评分</h4>\
<div class="waves-effect" onclick="editInfo(this)">\
  {starstr}\
</div>\
<select id="escore" style="display: none">\
  {starsel}\
</select>\
<h4>归档号</h4>\
<div class="waves-effect" onclick="editInfo(this)">{id_parsed}</div>\
<input id="eid" value="{paper_id}" type="text" class="form-control" style="display: none">\
<h4>链接</h4>\
<div><a href="{link}">{link}</a></div>';

var _Mauthor_b = '<span class="badge badge-primary m-1">{0}</span>'; // 作者打散显示

var _Mtopic_b = '<span class="badge badge-info m-1">{0}</span>'; // 题材打散

// 实心星星，半星，空心星星
var _Mstar_1 = '<i class="fas fa-star"></i>';
var _Mstar_half = '<i class="fas fa-star-half-alt"></i>';
var _Mstar_0 = '<i class="far fa-star"></i>';

function parseAuthors (la) {
    // 解析作者列表
    la = la.split(',');
    var alist = '';
    for(let i = 0;i < la.length; i++){
        alist += _Mauthor_b.format(la[i]);
    }
    return alist;
}

function parseTopics (info) {
    // 解析话题
    let ti = info.topic;
    let tn = ""+info.topic_name;
    tn = tn.split(',');
    var formatted_tlist = '';
    for (let i = 0; i < tn.length; i++) {
        const t = tn[i];
        formatted_tlist += _Mtopic_b.format(tn[i]);
    }
    return {
        'topic_parsed':formatted_tlist,
        'topic_s':tn.join(',')
    };
}

function parseScore (score) {
    // 图示化评分
    var s = parseInt(score);
    var starstr = '';
    var full = parseInt(s / 2);
    for (let f = 0; f < full; f++) {
        starstr += _Mstar_1;
    }
    if(s%2==1)starstr += _Mstar_half;
    for(let f = 0; f < 5-full-s%2; f++){
        starstr += _Mstar_0;
    }
    var starsel = '';
    for(let f = 0; f < 10; f++){
        if(f==score-1){
            starsel += '<option value="'+String(f+1)+'" selected="selected">'+String(f+1)+'</option>';
        }else{
            starsel += '<option value="'+String(f+1)+'">'+String(f+1)+'</option>';
        }
    }
    return {
        'starstr':starstr,
        'starsel':starsel
    };
}

function parseid (id) {
    // 解析paperid
    let idspl = id.split(':');
    if(idspl[0]=='doi'){
        return '<span class="badge badge-secondary">Doi</span>'+idspl[1];
    }else{
        return '<span class="badge badge-primary">arXiv</span>'+idspl[1];
    }
}
