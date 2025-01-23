import { nodeResolve } from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import replace from '@rollup/plugin-replace';

export default {
	input: './threejs-fiber.js',
	output: [
		{
			file: 'threejs-fiber.rollup.bundle.js',
			inlineDynamicImports: true,
			format: 'es'
		}
	],
	external: ["react", "react-dom", "react-reconciler", "react-reconciler/constant"],
	plugins: [
		replace({
			'process.env.NODE_ENV': JSON.stringify('production')
		}),
		nodeResolve({
			browser: true,
		}),
		commonjs({
			namedExports: {
				scheduler: [
					'unstable_runWithPriority',
					'unstable_IdlePriority',
					'unstable_now',
					'unstable_scheduleCallback',
					'unstable_cancelCallback',
				],
			}
		})
	],
};