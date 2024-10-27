<template>
	<view :class="container">
		<view :class="classContain1Obj">
			<view class="[box1, txt]">{{pointer}}</view>
		</view>
		<button type="default" @click="TurnRound()">击鼓传花</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				pointer: 0,
				classcontainer1: "container0",
				classContain1Obj: ""
			}
		},
		onLoad() {
			this.classContain1Obj = this.classcontainer1;
		},
		methods: {
			TurnRound() {
				this.pointer = (this.pointer + 1) % 9;
				console.log(this.pointer);
				this.classcontainer1 = 'container' + this.pointer;
				this.classContain1Obj = this.classcontainer1;
				console.log(this.classcontainer1);
			}
		}
	}
</script>

<style>
	.container {
		display: flex;
		flex-direction: row;
		margin: 10px;
	}

	.container0 {
		display: flex;
		width: 600rpx;
		height: 600rpx;
		background-color: beige;
		margin: 10rpx auto;
		justify-content: flex-start;
		align-items: flex-start;
	}
	.container1 {
		display: flex;
		width: 600rpx;
		height: 600rpx;
		background-color: beige;
		margin: 10rpx auto;
		justify-content: center;
		align-items: flex-start;
	}
	.container2 {
		display: flex;
		width: 600rpx;
		height: 600rpx;
		background-color: beige;
		margin: 10rpx auto;
		justify-content: flex-end;
		align-items: flex-start;
	}
	.container3 {
		display: flex;
		width: 600rpx;
		height: 600rpx;
		background-color: beige;
		margin: 10rpx auto;
		justify-content: flex-end;
		align-items: center;
	}
	.container4 {
		display: flex;
		width: 600rpx;
		height: 600rpx;
		background-color: beige;
		margin: 10rpx auto;
		justify-content: flex-end;
		align-items: flex-end;
	}
	.container5 {
		display: flex;
		width: 600rpx;
		height: 600rpx;
		background-color: beige;
		margin: 10rpx auto;
		justify-content: center;
		align-items: flex-end;
	}
	.container6 {
		display: flex;
		width: 600rpx;
		height: 600rpx;
		background-color: beige;
		margin: 10rpx auto;
		justify-content: flex-start;
		align-items: flex-end;
	}
	.container7 {
		display: flex;
		width: 600rpx;
		height: 600rpx;
		background-color: beige;
		margin: 10rpx auto;
		justify-content: flex-start;
		align-items: center;
	}
	.container8 {
		display: flex;
		width: 600rpx;
		height: 600rpx;
		background-color: beige;
		margin: 10rpx auto;
		justify-content: center;
		align-items: center;
	}
	.box1 {
		width: 200rpx;
		height: 200rpx;
		background-color: fuchsia;
		text-align: center;
		line-height: 200rpx;
	}
	.txt {
		font-size: 40rpx;
	}
</style>
