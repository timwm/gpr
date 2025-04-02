import React from 'react'
import Logo from './Logo.webp'
import CircleNotificationsIcon from '@mui/icons-material/CircleNotifications';
import AccountCircleIcon from '@mui/icons-material/AccountCircle'
function Header() {
  return (
   <>
    
        <header/>
        <div className='flex items-center justify-between p-4 bg-blue-600 text-white shadow-2xl' >
          {/*logo*/}
          <div className='flex items-center bg-blue-600'>
            <img src={Logo} className="App-logo rounded-full" alt="Logo" width={70}/>
            <h2 className='text-3xl font-bold p-3'>AITS</h2>
        
          
         
        </div>

        {/*searchbar*/}
        <input type="text" className='border-2 border-gray-300 p-2 w-664 rounded-3xl text-black outline-none' placeholder='Search'></input> 

        {/*Message*/}
        <h1 className='text-3xl'>ACADEMIC ISSUE TRACKING SYSTEM</h1>

        {/*icons*/}
        <div>
          <CircleNotificationsIcon className='mx-2 cursor-pointer'/>
          <AccountCircleIcon className ='mx-2 cursor-pointer'/>
        </div>
    </div>
    
   </>
  )
}

export default Header
