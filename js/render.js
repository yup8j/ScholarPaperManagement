let mainDiv = $('#main');
let libList = $('#libs');
let docList = $('#docs');
let docTable = $('#docTable');
let libListArea = $('#libList');

// 本地测试用
var masterURL = 'http://39.108.137.227/';

var dragImg = new Image(); 
dragImg.src = './img/file.jpg'; 

$(()=>{
    // 在线用户，替换'鸡你太美'
    var un = sessionStorage.getItem('username');
    if(un) $('#userName').html(un);
});

function getCurrentLibId() {
    // 获取现在的libid
    return libListArea.children('.active').attr('lid');
}

function getCurrentLibType() {
    // 获取现在的libid
    return libListArea.children('.active').attr('ltype');
}

function updateLibs () {
    // 获取liblist列表并绘制
    var libs = post_getLib();
    if(!libs)return;
    var lid = getCurrentLibId();
    // 未选中任何lib，直接渲染
    renderLibTable(libs);
    if(lid){
        // 有选择的lib，必须保持
        libListArea.children('li').removeClass('active');
        libListArea.children('li[lid="'+lid+'"]').addClass('active');
    }
}

function getDocsIn(lid, ltype) {
    // 获得lid中的文档并绘制
    var docs = post_getDoc(lid, ltype);
    if(!docs)return;
    renderDocumentTable(docs);
}

+ function($) {
    // 拖放文件上传
    'use strict';

    var dropZone = document.getElementById('drop-zone');

    var startUpload = function(files) {
        var upload = new FormData();
        upload.append('data',files[0]);
        postFile(upload);
        $('#lupload').hide();
        $('#ltable').show();
    }

    dropZone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'upload-drop-zone';

        startUpload(e.dataTransfer.files)
    }

    dropZone.ondragover = function() {
        this.className = 'upload-drop-zone drop';
        return false;
    }

    dropZone.ondragleave = function() {
        this.className = 'upload-drop-zone';
        return false;
    }

}(jQuery);

function border(div) {
    // 鼠标移到色标上时描绘边框
    $(div).css({'border':'2px solid gray'});
}

function deborder(div) {
    // 鼠标移出色标时取消描绘边框
    $(div).css({'border':'none'});
}

function showLUpload(ltable, event) {
    // 文件拖入时隐藏列表显示上传
    if(event.dataTransfer.effectAllowed == 'copy')return;
    let lupload = $('#lupload');
    lupload.attr('lid', $(ltable).attr('lid'));
    $(ltable).hide();
    lupload.show();
}

function showinfo(button) {
    // 点击详情，显示文献信息
    let infoModal = $('#infoModal');
    let infoBody = $('#infoBody');
    infoBody.empty();
    let did = $(button).parent().parent().parent().attr('did');
    let info = getInfoFor(did);
    if(!info){
        networkWarn();
        return;
    }
    infoBody.attr('did', did);
    info.author_parsed = parseAuthors(info.author);
    var foo =  parseTopics(info);
    info.topic_parsed = foo.topic_parsed;
    info.topic_s = foo.topic_s;
    foo = parseScore(info.score);
    info.starstr = foo.starstr;
    info.starsel = foo.starsel;
    info.id_parsed = parseid(info['paper_id']);
    infoBody.append($(_Minfo.format(info)));
    infoModal.modal('show');
}

function editInfo (e) {
    // 点选信息，开始编辑
    $(e).hide();
    $(e).next().show();
}

function updateInfo(btn){
    // 更新分类信息
    var document_id = $('#infoBody').attr('did');
    var title = $('#etitle').val();
    var author = $('#eauthors').val().split(',');
    var year = $('#eyear').val();
    var source = $('#esource').val();
    var score = $('#escore').val();
    var id = $('#eid').val();
    post_updateInfo({
        'document_id':document_id, 
        'title':title,
        'author':author,
        'year':year,
        'source':source,
        'score':score,
        'paper_id':id
    });
}

function hideLUpload(lupload) {
    // 文件没拖入时隐藏上传显示列表
    $(lupload).hide();
    $('#ltable').show();
}

function networkWarn () {
    // 显示一个网络错误的对话框
    $('#neterrModal').modal('show');
}

function promptSuccess(prompt) {
    // 返回一个提示操作已经成功的函数，提示词prompt
    return ()=>{
        console.log('ok')
        $('#successBan').html(prompt);
        $('#successBan').slideDown();
        setTimeout(()=>$('#successBan').slideUp(), 1000);
    }
}

function tooltipInit () {
    $('[data-toggle="tooltip"]').tooltip()
}

function maintaince () {
    let mheight = mainDiv.innerHeight();
    libList.height(mheight);
    docList.height(mheight);
    docList.width(mainDiv.innerWidth()-libList.outerWidth()-8);
    tooltipInit();
}

$(()=>{$('#lupload').hide();});

$(maintaince);

$(window).resize(maintaince);

$(function () {
    $('#dtDynamicVerticalScrollExample').DataTable(dttLocale);
    $('.dataTables_length').addClass('bs-select');
});

$(function(){
    // renderLibTable(dumbLibs.libs);
    // renderDocumentTable(dumbDocs.docs);
    updateLibs();
    libListArea.children('li[lid="1"]').addClass('active');
    getDocsIn('1', '1');
});

function dataTableTrun () {
    // 清空datatable
    let dtt = $('#dtDynamicVerticalScrollExample').dataTable();
    dtt.fnClearTable();
    dtt.fnDestroy();
}

function dataTableInit () {
    // 重新渲染datatable
    $('#dtDynamicVerticalScrollExample').dataTable(dttLocale);
    $('.dataTables_length').addClass('bs-select');
}

function createLib(btn) {
    // 添加分类
    var libname = $('#libName').val();
    post_createLib(libname);
}

function readDoc(td){
    // 点击阅读
    let did = $(td).parent().attr('did');
    sessionStorage.setItem('did',did);
    window.open('./read.html');
}

function addToReadLater(btn) {
    // 加到待读列表
    let did = $(btn).parent().parent().parent().attr('did');
    post_addToReadLater(did);
}

function showDocsIn (li) {
    // 点击lib时，激活此li并显示lib内容到右侧
    libListArea.children('li').removeClass('active');
    $(li).addClass('active');
    getDocsIn($(li).attr('lid'), $(li).attr('ltype'));
}

function changeMark(td) {
    let markModal = $('#markModal');
    markModal.attr('did', $(td).parent().attr('did'));
    markModal.modal('show');
}

function changeMarkTo (m) {
    // 改变分类为m
    let did = $('#markModal').attr('did');
    post_changeMark(did, m);
}

function delLib (btn) {
    // 删除library
    let lid = $(btn).parent().attr('lid');
    let m = $('#warnDelLibModal');
    m.attr('lid',lid);
    m.modal('show');
    hideDelLibBtn('#showDelLibBtn');
}

function delLibConfirmed (btn) {
    let lid = $(btn).parent().parent().parent().parent().attr('lid');
    // 实际操作删除分类
    post_delLib(lid);
}

function dragDoc(tr, event) {
    // 开始拖动文献
    event.dataTransfer.setData('Text',$(event.target).parent().attr('did'));
    event.dataTransfer.effectAllowed = 'copy';
    event.dataTransfer.setDragImage(dragImg, 64, 64);
    event.target.style.backgroundColor = 'cyan';
}

function dragDocOk (event) {
    event.target.style.backgroundColor = '';
}

function allowDrop(li, event) {
    $(li).css('border','2px solid');
    event.preventDefault();
}

function docOut (li) {
    $(li).css('border', '1px solid rgba(0,0,0,.125)');
}

function receiveDoc (li, event) {
    // 文献被拖到新的分类
    let lid = $(li).attr('lid');
    var did = event.dataTransfer.getData("Text");
    docOut(li);
    post_addDocToLib(did, lid);
}

function down(button) {
    // 下载文献
    let did = $(button).parent().parent().parent().attr('did');
    window.open(masterURL+'getdoc/'+did);
}

function remFromLib(button) {
    // 从分类中移除一篇文献
    if(getCurrentLibId=='1' || getCurrentLibType=='1')return;
    let did = $(button).parent().parent().parent().attr('did');
    var lid = getCurrentLibId();
    post_remDocFromLib(did, lid);
}

function showDelLibBtn (btn) {
    // 显示删除分类的按钮
    $('#libList').children('li').children('button').show();
    $(btn).removeClass('btn-outline-secondary');
    $(btn).addClass('btn-danger');
    $(btn).attr('onclick','hideDelLibBtn(this);');
    tooltipInit();
}

function hideDelLibBtn (btn) {
    // 隐藏删除分类的按钮
    $('#libList').children('li').children('button').hide();
    $(btn).removeClass('btn-danger');
    $(btn).addClass('btn-outline-secondary');
    $(btn).attr('onclick','showDelLibBtn(this);');
    tooltipInit();
}

function delDoc(delBtn){
    // 彻底删除文献
    let warnModal = $('#warnRemDocModal');
    warnModal.attr('did', $(delBtn).parent().parent().parent().parent().attr('did'));
    warnModal.modal('show');
}

function delDocConfirmed(btn) {
    // 处理删除文献
    let did = $('#infoBody').attr('did');
    post_removeDoc(did);
    $('#warnRemDocModal').modal('hide');
    $('#infoModal').modal('hide');
}

function renderLibTable(larray) {
    // 把列表larray渲染到分类目录
    libListArea.empty(); // 先清空dom
    var list = [];
    var all, rl; // 全部和待读
    for (let i = 0; i < larray.length; i++) {
        const lib = larray[i];
        if(lib.type==0){
            lib.lib_name = '<i class="fas fa-flag"></i>待读列表';
            rl = $(_Mlib_0.format(lib));
        }
        else if(lib.type==1){
            lib.lib_name = '<i class="fas fa-folder-open"></i>所有文献';
            all = $(_Mlib_1.format(lib));
        }
        else {
            var li = $(_Mlib.format(lib));
            list.push(li);
        }
    }
    libListArea.append(all);
    libListArea.append(rl);
    libListArea.append(list);
    tooltipInit();
}

function renderDocumentTable(darray) {
    // 把文献列表渲染到docTable
    docTable.empty();
    dataTableTrun();
    var isAll = (getCurrentLibId()=="1" || getCurrentLibType()=="1");
    for (let i = 0; i < darray.length; i++) {
        const doc = darray[i];
        doc.mark = markColours[doc.mark];
        // 如果分类为所有文献那么不渲染移除按钮
        if(isAll)doc.remove_btn = '';
        else doc.remove_btn = _MRemoveDoc;
        docTable.append($(_Mdoc.format(doc)));
    }
    dataTableInit();
    tooltipInit();
}
