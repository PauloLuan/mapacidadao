function reset_form_ajax(){
  var options = {target:$('#containers')};
  $('.ajax-comment-form').ajaxForm(options);
}
function init_mapa() {
    var options = {
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:900913"),
        units: "m",  numZoomLevels: 18, maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(-20037508, -20037508, 20037508, 20037508.34),
        restrictedExtent: new OpenLayers.Bounds(-5179137.4061623998, -2676741.9745125002, -5037435.7930119997, -2625236.0547225)
    };              
   
    
    mapa = new OpenLayers.Map('mapa', options);
    var gstr = new OpenLayers.Layer.Google("Mapa",{'sphericalMercator': true});
    mapa.addLayer(gstr);
    
    uomoLayer = new OpenLayers.Layer.Vector("uomoLayer", options);
    mapa.addLayer(uomoLayer);   
    
    
    var ghyb = new OpenLayers.Layer.Google("Híbrido", {
       type: G_HYBRID_MAP, 
       'sphericalMercator': true});
    mapa.addLayer(ghyb);
    
    
  
    var stylesMap = new OpenLayers.StyleMap({
            "default": new OpenLayers.Style({
                pointRadius:22,
                fillColor: "#ffcc66",
                strokeColor: "#ff9933",
                strokeWidth: 3,
                fillOpacity: 1,
            strokeColor: "#ff5555",
            externalGraphic: "${getExternalGraphic}",
            graphicWidth:21, graphicHeight:22, graphicYOffset:-22
            }, 
            {
       context: {
           getExternalGraphic:function(feature) {
               if (feature.attributes.icon_name == "")
                   return  img_base_path + "icons/cone_border.png";
               // Red if state is false
               else
                   return  img_base_path + "/icons/" + feature.attributes.icon_name;
           }
       }    
   }
            ),
            "select": new OpenLayers.Style({
                fillColor: "#66ccff",
                strokeColor: "#3399ff",
                graphicZIndex: 2
            })
        });

    var lixo = new OpenLayers.Layer.Vector("KML", {
        styleMap:stylesMap,
        rendererOptions: {zIndexing: true},
        projection: mapa.displayProjection,
        strategies: [new OpenLayers.Strategy.Fixed()],
        protocol: new OpenLayers.Protocol.HTTP({
            url: url_markers_kml,
            format: new OpenLayers.Format.KML({
                extractStyles: false,
                extractAttributes: true
            })
        })
    });
    mapa.addLayer(lixo);
    
   
    select = new OpenLayers.Control.SelectFeature(lixo);
    lixo.events.on({
        "featureselected": onFeatureSelect,
        "featureunselected": onFeatureUnselect
    });
    
    
    mapa.addControl(select);
    select.activate();  
    
    function onPopupClose(evt) {
        select.unselectAll();
    }
    


    function onFeatureSelect(event) {
        var feature = event.feature;
        // Since KML is user-generated, do naive protection against
        // Javascript.
        //$('#context-content').load('mapa/ponto/detail/'+feature.attributes.id, function(){reset_form_ajax();});
        var content = "<h3 style=\"margin:3px;\color:#F29B20;\">"+feature.attributes.name + "</h3>";
        content += "<div style=\"color:#5E8247;\">";
        if(feature.attributes.thumbnail!='') {
            content += '<img src="'+feature.attributes.thumbnail+'" align="left" style="margin-right:5px; margin-bottom:5px;" />';
        }
        content += feature.attributes.description + "</div>"+"<br/><b>Votos:</b>"+ feature.attributes.votos + "<br/><a href=\"mapa/ponto/detail/" +feature.attributes.id + "\/\"> Veja detalhes </a><br/><br/>";
        content += '<iframe src="http://www.facebook.com/plugins/like.php?href=www.mapadocidadao.com.br/mapa/ponto/detail/'+feature.attributes.id+'/&amp;layout=button_count&amp;show_faces=true&amp;width=100&amp;action=like&amp;font=arial&amp;colorscheme=light&amp;height=21" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:100px; height:21px;" allowTransparency="true"></iframe>';
        content += '<iframe allowtransparency="true" frameborder="0" scrolling="no" src="http://platform.twitter.com/widgets/tweet_button.html?url=http%3A%2F%2Fwww.mapadocidadao.com.br%2Fmapa%2Fponto%2Fdetail%2F'+feature.attributes.id+'%2F&amp;count=horizontal&amp;counturl=http%3A%2F%2Fwww.mapadocidadao.com.br%2Fmapa%2Fponto%2Fdetail%2F'+feature.attributes.id+'%2F&amp;text=Novo Relato | Mapa do Cidadão - '+feature.attributes.name+':&amp;related=mapacidadao:Mapa do Cidadão&amp;via=mapadocidadao" style="width:100px; height:20px;"></iframe>';
        if (content.search("<script") != -1) {
            content = "Content contained Javascript! Escaped content below.<br />" + content.replace(/</g, "&lt;");
        }
        popup = new OpenLayers.Popup.FramedCloud("chicken", 
                                 feature.geometry.getBounds().getCenterLonLat(),
                                 new OpenLayers.Size(100,100),
                                 content,
                                 null, true, onPopupClose);
        feature.popup = popup;
        
        mapa.addPopup(popup);
        
    }
    function onFeatureUnselect(event) {
        var feature = event.feature;
        if(feature.popup) {
            mapa.removePopup(feature.popup);
            feature.popup.destroy();
            delete feature.popup;
        }
    }

    // PONTO EDICAO
    var pointLayer = new OpenLayers.Layer.Vector("edit_point");
    mapa.addLayer(pointLayer);
    control_point = new OpenLayers.Control.DrawFeature(pointLayer,OpenLayers.Handler.Point);
    feature_point = new OpenLayers.Control.SelectFeature(pointLayer);
    mapa.addControl(feature_point);
    //feature_point.deactivate();   
    mapa.addControl(control_point);

    
    function get_ewkt (feat){wkt_f = new OpenLayers.Format.WKT();return 'SRID=900913;' + wkt_f.write(feat);}
    function write_wkt(feat){document.getElementById('id_ponto').value = get_ewkt(feat);}
    function add_wkt(event){
        //alert(event.type);
        if (pointLayer.features.length > 1){
            //alert(pointLayer.features.length);
            old_feats = [pointLayer.features[0]];
            pointLayer.removeFeatures(old_feats);
            pointLayer.destroyFeatures(old_feats);
        }
        write_wkt(event.feature);
        mapa.setCenter(new OpenLayers.LonLat(event.feature.geometry.x, event.feature.geometry.y ),17)
    }
    pointLayer.events.on({"featureadded" : add_wkt});

//    {% if extent %}
//    mapa.zoomToExtent(new OpenLayers.Bounds{{ extent }});
//    {% else %}        
    if (!mapa.getCenter()) {mapa.zoomToMaxExtent();}
//    {% endif %}     
}


var geocoder = new GClientGeocoder();

function showAddress(address) {
    var uomoStyle = { graphicWidth: 25,graphicHeight: 28,graphicYOffset:-28,graphicXOffset:-7, externalGraphic:img_base_path + "uomo_stick_25X28.png"};
        
    geocoder.getLatLng('São josé dos campos' + address,
        function(point) {
            if (!point) {
                alert(address + "não foi encontrado.!");
            } 
            else {
               address_point = new OpenLayers.LonLat(point.x,point.y).transform(new  OpenLayers.Projection("EPSG:4326"), mapa.getProjectionObject());
               mapa.setCenter(address_point, 17);
               adressFeature = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Point(address_point.lon, address_point.lat),null ,uomoStyle);
               uomoLayer.addFeatures(adressFeature);
            }
         }
    );
}