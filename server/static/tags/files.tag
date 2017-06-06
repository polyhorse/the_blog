<files>

	<div class='container'>
		<div class="columns">
			<div class='col-12'>

				<div class="divider"/>

				<!-- <progress class="progress" max="100"></progress> -->
				<form onsubmit={ create_new_slide } method=post enctype=multipart/form-data >
					<div class="input-group">
						<input ref="input" type="file" class="form-input" name='file'>
						<input type='hidden' name='count' value='{items.length}'>
						<button class="btn btn-primary input-group-btn btn-lg" style="min-width:120px">Upload</button>
					</div>
				</form>

				<div class="divider"/>

				<div class="input-group" each={items} style='margin-top: 1rem'>

					<div class="card" style='padding:8px;background-color:#f6f6f6;margin-top:12px'>
						<div class="card-image">
							<img src="{image_root+filename}" class="img-responsive" />
						</div>

						<div class="card-footer">
							<div class="btn-group btn-group-block">
								<button class="btn btn-primary btn-lg" show={can_edit} onclick={delete_slide}><i class='icon icon-cross'/> delete</button>
								<button class="btn btn-primary btn-lg" onclick={decrement_slide} show={order>0}><i class='icon icon-arrow-down' /> Move Down</button>
								<button class="btn btn-primary btn-lg" onclick={increment_slide} show={order<this.items.length-1}><i class='icon icon-arrow-up' /> Move Up</button>
							</div>
						</div>

					</div>

				</div>
		

			</div><!--end column 8-->

		</div><!--end all columns -->
	</div><!--end container-->

</files>