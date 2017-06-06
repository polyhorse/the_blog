<settings>

	<div class='container'>
		<div class="columns">
			<div class='col-12'>

				<div class='container' style='margin-top: 1rem'>
					<div class="columns">
							<div class='col-4'/>
							<div class='col-4'>
								<div class="loading" show={is_loading}></div>
							</div>
							<div class='col-4'/>
					</div>
				</div>

				<form class="form-horizontal">
					<div class="form-group">
						<div class="col-12">
							<label class="form-switch">
								<input type="checkbox" onclick={ show_stat_did_change } checked={this.items.auto_show_stat_on_change}/>
								<i class="form-icon"></i> Show Stats immediately after change to slides or stat settings
							</label>
						</div>
					</div>
					<div class="input-group" style='    margin-top: 1rem'>
						<span class="input-group-addon addon-lg" style='min-width:120px'>Slide Duration</span>
						<input type="number" class="form-input input-lg" placeholder="enter a number" onkeyup={slide_duration_did_change} value={this.items.slide_duration}/>
					</div>
					<div class="input-group" style='    margin-top: 1rem'>
						<span class="input-group-addon addon-lg" style='min-width:120px'>Stats Every</span>
						<input type="number" class="form-input input-lg" placeholder="number" onkeyup={adoption_stats_did_change} value={this.items.stat_frequency}/>
						<span class="input-group-addon addon-lg" style='min-width:120px'>slide(s)</span>
					</div>
					<div class="input-group" style='    margin-top: 1rem'>
						<span class="input-group-addon addon-lg" style='min-width:120px'>Flickr User ID</span>
						<input type="text" class="form-input input-lg" placeholder="number" onkeyup={flickr_id_did_change} value={this.items.flickr_user_id}/>
						<span class="input-group-addon addon-lg" style='min-width:120px'>slide(s)</span>
					</div>


					<!-- form select control -->

					<div class="input-group" style='    margin-top: 1rem'>
						<span class="input-group-addon addon-lg" style='min-width:120px;max-width:120px'>Flickr album</span>
						<select ref="album_selector" class="form-select " style='width:100%;height:45px'  onchange={flickr_album_did_change} value="72157678858148404">
							<option value='None' >Choose An Album</option>
							<option value={id} each={flicker_albums} selected='{id == items.flickr_album }'>{title._content}</option>
						</select>
					</div>
					
				</form>






			</div><!--end column 8-->

		</div><!--end all columns -->
	</div><!--end container-->


	<script>
	this.flicker_albums = [{title:''}]

	this.items = {
		auto_show_stat_on_change:false,
		slide_duration:0,
		stat_frequency:0
	}

		this.is_loading = false
		this.get_data = fetchival(window.location.origin+'/api/v1/get/settings')
		this.post_data = fetchival(window.location.origin+'/api/v1/update/settings')
		this.delete_data = fetchival(window.location.origin+'/api/v1/delete/settings')

		toggle_edit_mode(e){
			this.can_edit = e.target.checked
		}
		hide_status(){
			this.is_loading = false
			this.update()
		}
		show_status(){
			this.is_loading = true
			this.update()
		}

		fetch_data(){
			this.show_status()
			this.get_data.get().then(this.recieved_data)
		}

		recieved_data(data){
			if(data.status == 'good'){
				this.items = data.query
				this.flicker_albums = data.flicker_albums
				// if(this.items.flickr_album){
				// 	console.log(this.refs.album_selector.value+":"+this.items.flickr_album)
				// 	this.refs.album_selector.value = this.items.flickr_album
				// 	console.log(this.refs.album_selector)
				// 	this.update()
				// }
				
				// console.log(this.items)
				this.update();
			}else{
				// console.log(data.status)
			}
			setTimeout(this.hide_status, 1000)
		}

		delete_slide(e){
			this.delete_data.post(e.item).then(this.fetch_data())
		}

		save_settings(){
			this.show_status()
			this.post_data.post(this.items).then(this.parse_settings_update_response)
		}

		parse_settings_update_response(data){
			if(data.query.length>0){
				this.flicker_albums = data.query
			}
			// this.update()
			setTimeout(this.hide_status, 1000)
		}

		set_delayed_update(item){
			clearTimeout(this.delayed_update)
			this.delayed_update = setTimeout(this.save_settings, 1000)
		}

		show_stat_did_change(event){
			this.items.auto_show_stat_on_change = event.target.checked
			this.set_delayed_update()
		}

		slide_duration_did_change(event){
			this.items.slide_duration = event.target.value
			this.set_delayed_update()
		}

		adoption_stats_did_change(event){
			this.items.stat_frequency = event.target.value
			this.set_delayed_update()
		}

		flickr_id_did_change(event){
			this.items.flickr_user_id = event.target.value
			this.set_delayed_update()
		}

		flickr_album_did_change(event){
			this.items.flickr_album = event.target.value
			console.log(this.items.flickr_album)
			this.set_delayed_update()
		}

		did_select_album(event){
			console.log(event.target.value)
		}

		create_new_slide(e){
			
		}

		this.on('updated', this.fetch_data());

	</script>

</settings>