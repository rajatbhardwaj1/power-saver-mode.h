import React from 'react';
import './chat.css';
import { ReactSession } from 'react-client-session';
import axios from 'axios';
import { useFormik} from 'formik';
import Chat from './chat';
import data from './data.js';

function Report(props) {
	const [render, setRender] = React.useState(true);
	const [messages, setMessages] = React.useState([])
	const [inc, setinc] = React.useState(0);


	ReactSession.setStoreType("localStorage");
	const token = ReactSession.get("access_token")
	// const getMessages = () => axios.get(`https://testapi.tryst-iitd.org/api/users/messages/`, {
	// 		headers: { 'Authorization' : `Bearer ${token}` }
	// 	}).then((response) => setMessages(response.data));

	React.useEffect(() => {
		if (!render) return;
		setRender(false);
		// getMessages();
		setMessages(data);
	},[inc]);
	

	const {values, resetForm, handleBlur, handleSubmit, handleChange} = useFormik({
		initialValues: {text: ''},
		enableReinitialize: true,
		onSubmit: (values)=>{
			if(values.text.length !== 0){
				console.log(values.text);
				// axios.post(`https://testapi.tryst-iitd.org/api/users/messages/`, {
				// 	message: values.text
				// },
				// {
				// 	headers: {
				// 		'Authorization': `Bearer ${token}`
				// 	}
				// }
				// ).then((response) => {
				// 	resetForm({text: ''})
				// 	// getMessages();
				// 	setinc((pre) => pre+1);
				// });
			}
		},
	});
	return (
		<React.Fragment>
			<div className='user-chat-div' >
				<Chat messages={messages} />
				<div className='report-text-area'>
					<div>
						<form onSubmit={handleSubmit} method='post' className='report-input'>
							<input
								type='text'
								name='text'
								autoComplete='off'
								value={values.text}
								onChange={handleChange}
								onBlur={handleBlur}
								placeholder='Type your message here'
							></input>
							<button className='chat-btn' type='submit'>
								<svg width='21' height='18' viewBox='0 0 41 36' fill='none' xmlns='http://www.w3.org/2000/svg'>
									<path
										d='M0 33.1662V2.83289C0 1.97734 0.35 1.32556 1.05 0.87756C1.75 0.431116 2.48889 0.363448 3.26667 0.674559L39.2 15.8412C40.1722 16.269 40.6583 16.9884 40.6583 17.9996C40.6583 19.0107 40.1722 19.7301 39.2 20.1579L3.26667 35.3246C2.48889 35.6357 1.75 35.5672 1.05 35.1192C0.35 34.6728 0 34.0218 0 33.1662ZM4.66667 29.6662L32.3167 17.9996L4.66667 6.33289V14.4996L18.6667 17.9996L4.66667 21.4996V29.6662Z'
										fill='#93FFD8'
									/>
								</svg>
							</button>
						</form>
					</div>
				</div>
			</div>
		</React.Fragment>
	);
}
export default Report;
