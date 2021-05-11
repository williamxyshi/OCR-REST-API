/* This example requires Tailwind CSS v2.0+ */
import Hero from './Hero'
import Pricing from './Pricing'
import HeaderBar from './HeaderBar'

export default function LandingPage() {
  return (
    <div>
        <HeaderBar/>
        <Hero />
        <Pricing />
    </div>
  ) 
}